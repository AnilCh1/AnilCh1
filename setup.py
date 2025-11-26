import os
import subprocess
import sys

def install_requirements():
    """Automatically install required packages"""
    print("📦 Installing required packages...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
    except subprocess.CalledProcessError:
        print("❌ Failed to install packages. Please run: pip install -r requirements.txt")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    install_requirements()
    print("\n🎉 Setup complete! Now run: python app.py")
    print("🌐 Then open your browser to: http://localhost:5000")