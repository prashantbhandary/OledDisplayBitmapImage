# animationDisplay

Simple ESP32 + SSD1306 OLED project that displays a bitmap image on a 128x64 screen.

## What This Project Does

This project:
- Initializes an SSD1306 OLED display over I2C.
- Loads a bitmap stored in firmware (`myBitmap`).
- Draws the bitmap at boot and keeps it on screen.

Current behavior is a static image display (not a frame-by-frame animation engine yet).

## Tech Stack

- PlatformIO
- Arduino framework for ESP32
- Adafruit libraries:
  - Adafruit SSD1306
  - Adafruit GFX
  - Adafruit BusIO

These libraries are vendored in the `lib/` folder, so the project can build without fetching them externally.

## Project Structure

- `src/main.cpp`: Main firmware logic and bitmap data.
- `platformio.ini`: PlatformIO board/framework configuration (`esp32dev`, Arduino).
- `pythonscripts/convert_image.py`: Converts image files to C bitmap arrays for OLED rendering.
- `pythonscripts/bitmap_output.txt`: Generated output sample from converter script.
- `lib/`: Local copies of Adafruit display dependencies.
- `include/`, `test/`: Standard PlatformIO folders.

## Hardware Assumptions

- Board: ESP32 Dev Module (`esp32dev`)
- Display: SSD1306 128x64 I2C OLED
- I2C Address: `0x3C`

Typical ESP32 I2C pins:
- SDA: GPIO 21
- SCL: GPIO 22

If your wiring or display address differs, update initialization code in `src/main.cpp`.

## Build and Upload

1. Install PlatformIO (VS Code extension or CLI).
2. Connect ESP32 via USB.
3. From project root, run:

```bash
pio run
pio run -t upload
pio device monitor -b 115200
```

## How Image Rendering Works

In `src/main.cpp`:
1. `display.begin(...)` initializes OLED.
2. `display.clearDisplay()` clears framebuffer.
3. `display.drawBitmap(0, 0, myBitmap, 128, 64, WHITE)` places bitmap.
4. `display.display()` pushes framebuffer to OLED.

The bitmap array is stored as:

```cpp
const unsigned char myBitmap[] PROGMEM = { ... };
```

`PROGMEM` keeps large bitmap data in program memory.

## Converting Your Own Image

Use the Python converter in `pythonscripts/convert_image.py`.

### Requirements

```bash
pip install pillow
```

### Usage

```bash
cd pythonscripts
python3 convert_image.py path/to/image.png 128 64
```

Optional invert mode:

```bash
python3 convert_image.py path/to/image.png 128 64 --invert
```

The script prints C code and writes `bitmap_output.txt`.

### Replace the Displayed Image

1. Generate bitmap output with the script.
2. Copy generated `const unsigned char myBitmap[] PROGMEM = { ... };`
3. Replace existing `myBitmap` array in `src/main.cpp`.
4. Rebuild and upload.

## Common Customizations

- Change display resolution:
  - Update `SCREEN_WIDTH`, `SCREEN_HEIGHT`
  - Regenerate bitmap using matching dimensions
- Change I2C address:
  - Update `SCREEN_ADDRESS`
- Draw multiple images/frames:
  - Add additional bitmap arrays and call `drawBitmap` in `loop()`

## Troubleshooting

- Nothing on display:
  - Verify power and GND.
  - Check SDA/SCL pin mapping.
  - Confirm I2C address (`0x3C` vs `0x3D`).
- Build errors for display libs:
  - Ensure `lib/` folder is present and intact.
- Image looks wrong:
  - Regenerate bitmap at exact OLED resolution.
  - Try `--invert` option.

## Future Improvements (Suggested)

- Move bitmap arrays into separate header files.
- Add frame sequencing in `loop()` for actual animation.
- Add brightness/contrast and transition effects.
- Add serial commands for runtime image switching.

## License

No top-level license file is currently provided in this repository.
Check individual third-party libraries inside `lib/` for their licenses.
