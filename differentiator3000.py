import sys
import traceback
import cv2


def show_exception_and_exit(exc_type, exc_value, tb):
    traceback.print_exception(exc_type, exc_value, tb)
    input("Press key to exit.")
    sys.exit(-1)


sys.excepthook = show_exception_and_exit

# костанты
HAS_COLOR = '--color' in sys.argv
TAKE_CAMERA_VIDEO = '--cam' in sys.argv
FRAME_SKIP = 1
if TAKE_CAMERA_VIDEO:
    FRAME_SKIP = 1


# НЕОПТИМИЗИРОВАННАЯ функция нахождения разности между двумя кадрами
def abs_abs_diff(frame1: cv2.typing.MatLike, frame2: cv2.typing.MatLike):
    for i in range(0, frame2.shape[0] - 1, 2):
        for j in range(0, frame2.shape[1] - 1, 2):
            r1, g1, b1 = frame1[i, j]
            r2, g2, b2 = frame2[i, j]
            r = abs(int(r1) - int(r2))
            g = abs(int(g1) - int(g2))
            b = abs(int(b1) - int(b2))

            pixel = (r, g, b)
            frame2[i, j] = pixel
            frame2[i+1, j] = pixel
            frame2[i, j+1] = pixel
            frame2[i+1, j+1] = pixel


# проверочная функция
def frame_to_red(frame: cv2.Mat) -> cv2.Mat:
    for i in range(frame.shape[0]):
        for j in range(frame.shape[1]):
            frame[i, j] = (0, 255, 255)
    return frame


# функция, пропускающая n-1 кадров
def cap_mult_read(cap, n):
    for i in range(n - 1):
        cap.read()
    return cap.read()


# определение fps выходного видео
if '--fps' in sys.argv:
    FPS = int(sys.argv[sys.argv.index('--fps') + 1])
else:
    FPS = 30

# определение источника видео
if TAKE_CAMERA_VIDEO:
    cap = cv2.VideoCapture(0)
else:
    # проверка, есть ли входной файл
    if '--input' not in sys.argv:
        quit()
    file_path = sys.argv[sys.argv.index("--input") + 1]
    if file_path.split('.')[-1] != 'mp4':
        input('Есть поддержка только *.mp4 файлов...')
        quit()
    cap = cv2.VideoCapture(file_path)

# создание VideoWriter
codec = 'mp4v'
fourcc = cv2.VideoWriter_fourcc(*codec)
ret, frame1 = cap.read()
output_file_name = 'videoOutput\\' + sys.argv[sys.argv.index("--output") + 1].split('.')[0] + \
                   '_' + str(FPS) + '_' + codec + '.mp4'
out = cv2.VideoWriter(output_file_name,
                      fourcc,
                      FPS / FRAME_SKIP,
                      (int(cap.get(3)), int(cap.get(4))),
                      HAS_COLOR)

# обработка кадров видео/камеры
while cap.isOpened():
    # print(f'{frame1.shape[1]}, {frame1.shape[0]}')
    ret, frame2 = ret, frame1
    ret, frame1 = cap_mult_read(cap, FRAME_SKIP)
    if not ret:
        break

    if HAS_COLOR:
        abs_abs_diff(frame1, frame2)
        # frame = cv2.absdiff(frame1, frame2)
    else:
        frame = cv2.cvtColor(cv2.absdiff(frame1, frame2), cv2.COLOR_BGR2GRAY)

    cv2.imshow('Frame', frame2)
    # cv2.imshow('Orig', frame2)
    out.write(frame2)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
cap.release()
out.release()
cv2.destroyAllWindows()
