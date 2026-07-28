import pygame

class Animation:
    def __init__(self, image: pygame.Surface, size: int, fps: float):
        self.image = image
        self.size = size
        self.fps = fps
        self.images = []
        self.index = 0.0

        # Automatically calculate frames based on image width
        total_frames = image.get_width() // size
        
        for i in range(total_frames):
            # Slice each frame from the sheet
            frame_rect = pygame.Rect(i * size, 0, size, size)
            self.images.append(self.image.subsurface(frame_rect))

    def update(self, dt: float):
        self.index += self.fps * dt
        self.index %= len(self.images)

    def get_image(self):
        return self.images[int(self.index)]

class AnimationManager:
    def __init__(self, animations: dict[str, Animation], current_anim=None):
        self.animations = animations
        self.current_anim = current_anim

    def new_anim(self, name, anim):
        self.animations[name] = anim

    def change_anim(self, name):
        self.current_anim = name

    def update(self, dt: float):
        if self.current_anim is None and self.current_anim in self.animations:
            return
        self.animations[self.current_anim].update(dt)
    def get_image(self):
        if self.current_anim is None and self.current_anim in self.animations:
            return
        return self.animations[self.current_anim].get_image()

