import unittest
import main as m
import pygame

class Test_FontDisplay(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pass

    def tearDown(self) -> None:
        pygame.quit()

    def test_anykey(self):

        normal_key = [chr(c) for c in range(32,127)]
        print(normal_key)

        for c in normal_key:
            fd = m.FontDisplay(c)
            print(fd.char)

if __name__ == '__main__':
    unittest.main()