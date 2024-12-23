# File Server

A lightweight and user-friendly file server for uploading, managing, and sharing files within a local network. This server allows you to seamlessly upload files to a centralized server and share them with other devices connected to the same network.

---

## Features

- **File Upload**: Easily upload files to the server using a web interface or API.
- **File Sharing**: Share uploaded files with other devices on the same network via download links.
- **Simple Setup**: Quick and easy configuration for local network sharing.
- **Cross-Platform**: Works on Windows, macOS, and Linux systems.

---

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Required libraries (install with pip):
  - Flask
  - Flask-Cors

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/dpgaire/file-server.git
   cd file-server
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the server:
   ```bash
   python app.py
   ```

4. Access the server:
   Open your web browser and navigate to `http://<your-local-ip>:5000`.

---

## Configuration

- **Server Port**: By default, the server runs on port `5000`. You can change this in the `app.py` file.
- **Upload Directory**: Files are stored in the `uploads` folder by default. Update the folder path in the `app.py` file if needed.

---

## Usage

1. **Upload Files**:
   - Use the web interface to select and upload files.
   - Uploaded files are listed and can be downloaded using generated links.

2. **Share Files**:
   - Share the download link (e.g., `http://<your-local-ip>:5000/uploads/filename`) with others on the network.

---

## Security

- This server is designed for local network use. For internet-facing deployments, add proper authentication and encryption to secure the data.

---

## Contributing

We welcome contributions! If you find a bug or have a feature request, please open an issue. To contribute code:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -am 'Add feature-name'`).
4. Push to the branch (`git push origin feature-name`).
5. Create a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/).

---