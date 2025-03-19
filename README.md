# 🌐 ESP32-S3 IoT Project: Environment Monitor & Trivia Game

This project uses the **ESP32-S3** microcontroller programmed in **MicroPython** to implement two powerful and fun modules:

1. **Real-Time Temperature & Humidity Monitoring**
2. **Interactive Web-Based Trivia Game**

---

## 📦 Features

### 🧪 Module 1: Temperature & Humidity Monitoring
- Uses **DHT11** sensor to read temperature and humidity.
- Data served on a **real-time responsive web page**.
- View updates on browser or mobile via ESP32-hosted server.
- Optionally integrates with **Blynk** for mobile dashboards.

### 🎮 Module 2: Trivia Game
- ESP32-S3 hosts a fully interactive **web-based trivia game**.
- Stylish **animated UI** with background color changes based on guesses.
- Dynamic feedback like **"Well Done!"**, **"Try Again"**, etc.
- **OLED display** and **RGB LED** give visual responses.
- Randomized questions from a **larger trivia database**.

---

## 🔧 Hardware Used

- ✅ ESP32-S3 Board  
- ✅ DHT11 Sensor (for temperature & humidity)  
- ✅ OLED Display (I2C-based)  
- ✅ RGB LED  
- ✅ Micro-USB cable for flashing  
- ✅ (Optional) Blynk App for mobile monitoring

---

## 🛠️ Installation & Setup

### 1. Flash MicroPython Firmware to ESP32-S3
- Use [Thonny IDE](https://thonny.org/) or [esptool.py](https://github.com/espressif/esptool)
- Choose the correct MicroPython firmware for ESP32-S3.

### 2. Upload the Python Files
- Connect ESP32 to your PC via USB.
- Use Thonny or `ampy` to upload `.py` files (main, game logic, sensor code).

### 3. Access Web Interface
- Connect to the ESP32's Wi-Fi AP or your home Wi-Fi.
- Open the browser and go to the IP shown in the serial console.

---

## 📸 Screenshots (optional)
> *Include screenshots or GIFs of the web interface, mobile dashboard, trivia game screen, etc.*

---

## 💡 Future Ideas
- Add buzzer for correct/wrong answers
- Save scores to flash memory
- Add multiplayer quiz logic
- Cloud integration for sensor logging

---

## 📄 License
This project is open-source under the MIT License.

---

## 👨‍💻 Author

**Sheeraz**  
Passionate about IoT, Embedded Systems, and Creative Coding  
GitHub: [@Sheeraz-07](https://github.com/Sheeraz-07)
