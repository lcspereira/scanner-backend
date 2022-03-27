from wsgiref.validate import validator
from pydantic import BaseModel, Field, PrivateAttr
from typing import Optional, List
import sane
from PIL import Image
import base64
import io

class Scanner(BaseModel):
    name: str = Field(...)
    res: Optional[int] = Field(150, description="Scan resolution")
    mode: str = Field("Color", description="Scan mode")
    source: str = Field("Flatbed", description="Scanner source")
    format: str = Field("JPEG")
    _device: Optional[sane.SaneDev]
    _info: Optional[List[tuple]]

    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True
        underscore_attrs_are_private = True

    def init_scanner(self) -> None:
        """Initialize scanner and settings"""
        self._device = sane.open(self.name)
        self._device['res'] = self.res
        self._device['mode'] = self.mode
        self._device['source'] = self.source

    def scan(self) -> Image:
        """Scan image from scanner

        Returns:
            Image: The scanned image
        """
        img = self._device.scan()
        return img

    def to_base64(self, img: Image) -> str:
        """Convert image to base64

        Args:
            img (Image): Image to be converted

        Returns:
            str: base64 image
        """
        buff = io.BytesIO()
        img.save(buff, format=self.format)
        return base64.b64encode(buff.getvalue())