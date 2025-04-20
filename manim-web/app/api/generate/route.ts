import { NextResponse } from 'next/server';
import { exec } from 'child_process';
import { promisify } from 'util';
import fs from 'fs';
import path from 'path';
import os from 'os';

const execAsync = promisify(exec);

export async function POST(request: Request) {
  try {
    const formData = await request.formData();
    const files = formData.getAll('images') as File[];
    
    // Create a temporary directory
    const tempDir = path.join(os.tmpdir(), 'manim-input');
    fs.mkdirSync(tempDir, { recursive: true });
    
    // Save uploaded images
    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      const buffer = Buffer.from(await file.arrayBuffer());
      const filePath = path.join(tempDir, `input_${i}.png`);
      fs.writeFileSync(filePath, buffer);
    }
    
    // Create output directory
    const outputDir = path.join(os.tmpdir(), 'manim-output');
    fs.mkdirSync(outputDir, { recursive: true });
    
    // Create permanent output directory
    const permanentOutputDir = path.join(process.cwd(), 'output');
    fs.mkdirSync(permanentOutputDir, { recursive: true });
    
    // Get the absolute path to the Python script
    const scriptPath = path.join(process.cwd(), '..', 'manim_agent.py');
    
    if (!fs.existsSync(scriptPath)) {
      throw new Error('Manim agent script not found');
    }
    
    // Run Manim generation process
    const { stdout, stderr } = await execAsync(
      `python3 "${scriptPath}"`,
      {
        env: {
          ...process.env,
          INPUT_DIR: tempDir,
          OUTPUT_DIR: outputDir,
        },
        maxBuffer: 10 * 1024 * 1024, // 10MB buffer
      }
    );
    
    // Find the generated video
    const videoFiles = fs.readdirSync(outputDir).filter(file => file.endsWith('.mp4'));
    if (videoFiles.length === 0) {
      throw new Error('No video file generated');
    }
    
    const latestVideo = videoFiles.sort().pop()!;
    const videoPath = path.join(outputDir, latestVideo);
    
    // Read the video file
    const videoBuffer = fs.readFileSync(videoPath);
    
    // Save a copy to the permanent output directory
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const permanentVideoPath = path.join(permanentOutputDir, `tutorial_${timestamp}.mp4`);
    fs.writeFileSync(permanentVideoPath, videoBuffer);
    
    // Clean up temporary files
    fs.rmSync(tempDir, { recursive: true, force: true });
    fs.rmSync(outputDir, { recursive: true, force: true });
    
    // Return the video
    return new NextResponse(videoBuffer, {
      headers: {
        'Content-Type': 'video/mp4',
        'Content-Disposition': `attachment; filename="${latestVideo}"`,
      },
    });
    
  } catch (error) {
    console.error('Error:', error);
    return NextResponse.json(
      { error: error instanceof Error ? error.message : 'Failed to generate video' },
      { status: 500 }
    );
  }
} 