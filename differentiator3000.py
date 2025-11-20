import sys
import traceback
import cv2


FRAME_SKIP = 3
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
                      (int(cap.get(3)), int(cap.get(4))))
while cap.isOpened():
    ret, frame2 = ret, frame1
    ret, frame1 = cap_mult_read(cap, FRAME_SKIP)
    if not ret:
        break
    frame = cv2.absdiff(frame1, frame2)
    cv2.imshow('Frame', frame)
    out.write(frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
cap.release()
out.release()
cv2.destroyAllWindows()
