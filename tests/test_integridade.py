"""Testes estáticos que não exigem abrir a janela do Pygame."""
import ast
import struct
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class TestProjetoRUN(unittest.TestCase):
    def test_codigo_python_valido(self):
        ast.parse((ROOT / "RUN!.py").read_text(encoding="utf-8"))

    def test_sprites_png_presentes_e_validos(self):
        sprites = ["moto1.png", "carro 1.png", "carro 2.png", "carro 3.png", "pistas1.png", "pistas2.png", "pistas3.png"]
        for name in sprites:
            with self.subTest(name=name):
                raw = (ROOT / name).read_bytes()
                self.assertEqual(raw[:8], b"\x89PNG\r\n\x1a\n")
                width, height = struct.unpack(">II", raw[16:24])
                self.assertGreater(width, 0)
                self.assertGreater(height, 0)

    def test_fonte_preservada(self):
        raw = (ROOT / "FONTE GAME.ttf").read_bytes()
        self.assertTrue(raw.startswith((b"\x00\x01\x00\x00", b"OTTO")))

    def test_musica_opcional_sem_quebrar_o_jogo(self):
        source = (ROOT / "RUN!.py").read_text(encoding="utf-8")
        self.assertIn("if not music.is_file():", source)
        self.assertIn("start_original_music()", source)


if __name__ == "__main__":
    unittest.main()
