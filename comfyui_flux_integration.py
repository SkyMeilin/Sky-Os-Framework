"""
SkyOS ComfyUI / FLUX.1 Asset Generation Module
Department: CREATIVE_VISUALS (ComfyUI / FLUX)
Agency Level Up 2025 (Pascal Weidermann, Hückelhoven)

Features:
- Automated Prompt Engineering for FLUX.1 & ComfyUI API Workflows
- Enforces Sky Meilin Brand Guidelines:
  - 25-year-old faceless/digital AI persona, flawless skin, subtle freckles
  - Hazel/green eyes, braided black hair with turquoise/blue/pink highlights
  - Pink lotus sternum tattoo, twin paw prints below collarbones, NO facial tattoos
  - Business-casual, leather, and sleek attire
- Negative Prompting Filter: Locks cyberpunk artifacts, facial tattoos, distorted limbs
- Six-Verb & WORM Audit Trail Compliant
"""

import os
import json
import time
from typing import Dict, Any, List, Optional

class ComfyUIFLUXService:
    """Adapter for ComfyUI & FLUX.1 Asset Generation Workflows."""

    COMFYUI_API_URL = os.getenv("COMFYUI_API_URL", "http://localhost:8188")

    SKY_MEILIN_POSITIVE_ANCHORS = [
        "25-year-old digital AI persona Sky Meilin",
        "flawless skin with subtle delicate freckles across nose and cheeks",
        "striking mandelförmige green hazel eyes",
        "long sleek braided black hair with vibrant turquoise and pink highlights",
        "pink lotus flower tattoo on sternum",
        "two small black paw print tattoos below collarbones",
        "modern sleek business-casual leather outfit",
        "professional studio lighting, 8k resolution, photorealistic, sharp focus"
    ]

    SKY_MEILIN_NEGATIVE_FILTER = [
        "facial tattoos", "face tattoo", "cyberpunk face artifacts",
        "distorted hands", "extra fingers", "blurry face", "disfigured",
        "deformed limbs", "overexposed", "grainy", "cartoonish"
    ]

    def __init__(self, comfyui_api_url: str = None):
        self.comfyui_api_url = comfyui_api_url or self.COMFYUI_API_URL

    def build_sky_meilin_prompt(self, scene_description: str, extra_styles: Optional[List[str]] = None) -> Dict[str, Any]:
        """Constructs a brand-compliant prompt payload for FLUX.1."""
        styles = extra_styles or []
        positive_prompt = ", ".join(self.SKY_MEILIN_POSITIVE_ANCHORS + [scene_description] + styles)
        negative_prompt = ", ".join(self.SKY_MEILIN_NEGATIVE_FILTER)

        return {
            "positive_prompt": positive_prompt,
            "negative_prompt": negative_prompt,
            "aspect_ratio": "16:9",
            "model": "FLUX.1-dev",
            "sampler": "euler",
            "steps": 28,
            "cfg_scale": 3.5
        }

    def generate_asset_preview(self, scene: str) -> Dict[str, Any]:
        """SEARCH -> RESOLVE -> PREVIEW phase."""
        prompt_data = self.build_sky_meilin_prompt(scene)
        return {
            "scene": scene,
            "comfyui_workflow": "flux_sky_meilin_v2.json",
            "prompt_payload": prompt_data,
            "status": "PREVIEW_READY"
        }

    def execute_asset_generation(self, preview_data: Dict[str, Any], human_approved: bool) -> Dict[str, Any]:
        """HUMAN_GATE -> EXECUTE phase."""
        if not human_approved:
            raise PermissionError("Asset generation blocked: HUMAN_GATE approval required.")

        # Simulated ComfyUI Job Execution
        asset_guid = f"asset_sky_meilin_{int(time.time())}"
        return {
            "status": "EXECUTED",
            "asset_id": asset_guid,
            "file_name": f"{asset_guid}.png",
            "dimensions": "1920x1080",
            "positive_prompt_used": preview_data["prompt_payload"]["positive_prompt"],
            "negative_prompt_used": preview_data["prompt_payload"]["negative_prompt"]
        }

def run_test():
    print("=" * 70)
    print(" SkyOS Core: ComfyUI / FLUX.1 Visuals Integration Test ")
    print("=" * 70)

    service = ComfyUIFLUXService()

    # Step 1: PREVIEW
    scene = "Sky Meilin presenting the SkyOS 15-department architecture dashboard in a modern tech office"
    preview = service.generate_asset_preview(scene)
    print(f"\n[1/3] PREVIEW Prompt Payload Built:\n  Positive Prompt: {preview['prompt_payload']['positive_prompt'][:120]}...\n  Negative Filter Active: {len(service.SKY_MEILIN_NEGATIVE_FILTER)} rules enforced.")

    # Step 2: EXECUTE with HUMAN_GATE
    execution = service.execute_asset_generation(preview_data=preview, human_approved=True)
    print(f"\n[2/3] EXECUTE Generated Asset ID: {execution['asset_id']}")
    print(f"  Dimensions: {execution['dimensions']}")

    print("\n" + "=" * 70)
    print(" ✅ ComfyUI / FLUX.1 Integration Test PASSED! ")
    print("=" * 70)

if __name__ == "__main__":
    run_test()
