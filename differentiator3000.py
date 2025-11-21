import sys
import traceback
import cv2


HAS_COLOR = False


def abs_abs_diff(frame1: cv2.typing.MatLike, frame2: cv2.typing.MatLike):
    for i in range(0, frame2.shape[0], 2):
        for j in range(0, frame2.shape[1], 2):
            r1, g1, b1 = frame1[i, j]
            r2, g2, b2 = frame2[i, j]
            r = abs(r1 - r2)
            g = abs(g1 - g2)
            b = abs(b1 - b2)
            pixel = ((r + g + b) / 3, ) * 3
            frame2[i, j] = pixel
            frame2[i+1, j] = pixel
            frame2[i, j+1] = pixel
            frame2[i+1, j+1] = pixel


def frame_to_red(frame: cv2.Mat) -> cv2.Mat:
    for i in range(frame.shape[0]):
        for j in range(frame.shape[1]):
            frame[i, j] = (0, 255, 255)
    return frame


FRAME_SKIP = 1
a = sys.argv.index('--fps')
if a >= 0:
    FPS = int(sys.argv[a+1])
else:
    FPS = 30


def show_exception_and_exit(exc_type, exc_value, tb):
    traceback.print_exception(exc_type, exc_value, tb)
    input("Press key to exit.")
    sys.exit(-1)


def cap_mult_read(cap, n):
    for i in range(n - 1):
        cap.read()
    return cap.read()


sys.excepthook = show_exception_and_exit


print(sys.argv)

if (sys.argv.index("--input") < 0):
    quit

file_path = sys.argv[sys.argv.index("--input") + 1]
if (file_path.split('.')[-1] != 'mp4'):
    input('Есть поддержка только *.mp4 файлов...')
    quit

cap = cv2.VideoCapture(file_path)
# cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
ret, frame1 = cap.read()
out = cv2.VideoWriter(sys.argv[sys.argv.index("--output") + 1], fourcc, FPS / FRAME_SKIP,
                      (int(cap.get(3)), int(cap.get(4))), HAS_COLOR)
while cap.isOpened():
    # print(f'{frame1.shape[1]}, {frame1.shape[0]}')
    ret, frame2 = ret, frame1
    ret, frame1 = cap_mult_read(cap, FRAME_SKIP)
    if not ret:
        break
    # abs_abs_diff(frame1, frame2)

    if HAS_COLOR:
        frame = cv2.absdiff(frame1, frame2)
    else:
        frame = cv2.cvtColor(cv2.absdiff(frame1, frame2), cv2.COLOR_BGR2GRAY)

    cv2.imshow('Frame', frame)
    out.write(frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
cap.release()
out.release()
cv2.destroyAllWindows()
