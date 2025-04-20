# Manim Video Generator Web App

A web application that allows users to generate educational videos from images using Manim.

## Prerequisites

- Node.js 18+ and npm
- Python 3.8+
- Manim (installed via Homebrew on macOS)
- Anthropic API key

## Setup

1. Clone the repository and navigate to the project directory:
   ```bash
   git clone <repository-url>
   cd manim-web
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Create a `.env` file in the root directory with your Anthropic API key:
   ```
   ANTHROPIC_KEY=your_anthropic_api_key
   ```

4. Install Manim (on macOS):
   ```bash
   brew install manim
   ```

## Running the Application

1. Start the development server:
   ```bash
   npm run dev
   ```

2. Open your browser and navigate to `http://localhost:3000`

## Usage

1. Upload one or more images by dragging and dropping them into the upload area or clicking to select files
2. Click the "Generate Video" button
3. Wait for the video to be generated (this may take a few minutes)
4. Once complete, the video will be displayed and can be downloaded

## Features

- Drag and drop image upload
- Support for multiple image formats (PNG, JPG, JPEG)
- Real-time progress indication
- Error handling and user feedback
- Responsive design

## Troubleshooting

If you encounter any issues:

1. Ensure Manim is properly installed and accessible from the command line
2. Check that your Anthropic API key is valid and properly set in the `.env` file
3. Verify that the input images are in a supported format
4. Check the browser console and server logs for error messages

## License

MIT 