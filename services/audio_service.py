"""
Audio generation service using Abair.ie TTS
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional
import time
import glob
import os

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pydub import AudioSegment

from models.voice_config import VoiceConfig
from services.progress_observer import ProgressObserver, NoOpProgressObserver


class AudioService(ABC):
    """Abstract base class for audio generation services"""

    @abstractmethod
    def generate_audio(
        self, text: str, voice: VoiceConfig, output_dir: Path
    ) -> Optional[Path]:
        """
        Generate audio for the given text with specified voice

        Args:
            text: Text to synthesize
            voice: Voice configuration
            output_dir: Directory to save audio file

        Returns:
            Path to generated audio file, or None if failed
        """
        pass

    @abstractmethod
    def setup(self):
        """Setup the audio service (e.g., initialize browser)"""
        pass

    @abstractmethod
    def cleanup(self):
        """Cleanup resources (e.g., close browser)"""
        pass


class AbairAudioService(AudioService):
    """Audio generation service using Abair.ie website via Selenium"""

    def __init__(
        self,
        download_folder: Path,
        observer: Optional[ProgressObserver] = None,
        wait_timeout: int = 15,
    ):
        """
        Initialize Abair audio service

        Args:
            download_folder: Folder for downloaded audio files
            observer: Progress observer for status updates
            wait_timeout: Selenium wait timeout in seconds
        """
        self.download_folder = download_folder
        self.observer = observer or NoOpProgressObserver()
        self.wait_timeout = wait_timeout
        self.driver: Optional[webdriver.Chrome] = None
        self.wait: Optional[WebDriverWait] = None
        self.current_voice: Optional[VoiceConfig] = None

    def setup(self):
        """Initialize Selenium browser and navigate to Abair.ie"""
        from gui.selenium_utils import setup_selenium

        try:
            self.driver, self.wait = setup_selenium(str(self.download_folder))
            self.current_voice = None
        except Exception as e:
            raise RuntimeError(f"Failed to setup Selenium: {e}")

    def cleanup(self):
        """Close browser and cleanup"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None
            self.wait = None
            self.current_voice = None

    def generate_audio(
        self, text: str, voice: VoiceConfig, output_dir: Path
    ) -> Optional[Path]:
        """
        Generate audio using Abair.ie

        Args:
            text: Irish text to synthesize
            voice: Voice configuration (dialect, gender)
            output_dir: Directory for audio output

        Returns:
            Path to generated audio file or None if failed
        """
        if not self.driver or not self.wait:
            raise RuntimeError("AudioService not initialized. Call setup() first.")

        try:
            # Only update settings if voice changed
            if self.current_voice != voice:
                if not self._set_voice_settings(voice):
                    return None
                self.current_voice = voice

            # Clean old synthesis files
            self._clean_old_files(output_dir)

            # Generate audio
            audio_path = self._synthesize_and_download(text, output_dir)

            # Apply speed adjustment if needed
            if audio_path and voice.needs_speed_adjustment():
                audio_path = self._apply_speed_adjustment(
                    audio_path, voice.speed_multiplier()
                )

            return audio_path

        except Exception as e:
            self.observer.on_error(f"Audio generation failed: {e}")
            return None

    def _set_voice_settings(self, voice: VoiceConfig) -> bool:
        """Configure Abair.ie voice settings"""
        try:
            # Set Dialect
            select_xpath = "//div[./div/span[text()='Dialect']]/div/select"
            select_element = self.wait.until(
                EC.presence_of_element_located((By.XPATH, select_xpath))
            )
            dialect_select = Select(select_element)
            dialect_select.select_by_visible_text(voice.dialect)
            time.sleep(1)

            # Set Gender
            gender_xpath = f"//div[./div/span[text()='Gender']]/div/button[contains(text(), '{voice.gender}')]"
            gender_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, gender_xpath))
            )
            self.driver.execute_script("arguments[0].click();", gender_btn)
            time.sleep(1)

            # Set Voice for Kerry Male (Danny)
            if voice.dialect == "Kerry" and voice.gender == "Male":
                voice_xpath = "//div[./div/span[text()='Voice']]/div/button[contains(text(), 'Danny')]"
                voice_btn = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, voice_xpath))
                )
                self.driver.execute_script("arguments[0].click();", voice_btn)
                time.sleep(1)

            # Set Model (AI)
            model_xpath = (
                "//div[./div/span[text()='Model']]/div/button[contains(text(), 'AI')]"
            )
            model_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, model_xpath))
            )
            self.driver.execute_script("arguments[0].click();", model_btn)
            time.sleep(1)

            return True

        except Exception as e:
            self.observer.on_error(f"Failed to set voice settings: {e}")
            return False

    def _clean_old_files(self, output_dir: Path):
        """Remove old synthesis files"""
        for old_file in glob.glob(str(output_dir / "synthesis*")):
            try:
                os.remove(old_file)
            except:
                pass

    def _synthesize_and_download(self, text: str, output_dir: Path) -> Optional[Path]:
        """Synthesize text and download audio file"""
        try:
            # Enter text
            text_area = self.wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "textarea"))
            )
            text_area.clear()
            time.sleep(2)
            text_area.send_keys(text)
            time.sleep(2)

            # Click Synthesize
            synth_btn = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(., 'Synthesize')]")
                )
            )
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", synth_btn
            )
            time.sleep(2)
            synth_btn.click()
            time.sleep(5)

            # Click Download
            download_btn = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(., 'Download')]")
                )
            )
            time.sleep(2)
            before_click = time.time()
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", download_btn
            )
            download_btn.click()

            # Wait for file download
            return self._wait_for_download(output_dir, before_click)

        except Exception as e:
            self.observer.on_error(f"Synthesis failed: {e}")
            return None

    def _wait_for_download(
        self, output_dir: Path, after_timestamp: float, max_attempts: int = 30
    ) -> Optional[Path]:
        """Wait for audio file to download"""
        from gui.helpers import get_latest_file

        for _ in range(max_attempts):
            time.sleep(1)
            latest = get_latest_file(str(output_dir))
            if (
                latest
                and os.path.getmtime(latest) > after_timestamp
                and not latest.endswith(".crdownload")
            ):
                return Path(latest)

        return None

    def _apply_speed_adjustment(self, audio_path: Path, speed: float) -> Path:
        """Apply speed adjustment to audio file"""
        try:
            audio = AudioSegment.from_file(str(audio_path))
            adjusted = audio.speedup(playback_speed=speed)

            # Save to same path
            adjusted.export(str(audio_path), format="mp3")
            return audio_path

        except Exception as e:
            self.observer.on_error(f"Speed adjustment failed: {e}")
            return audio_path  # Return original on failure
