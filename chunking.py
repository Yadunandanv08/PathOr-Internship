class ChunkManager:
    def __init__(self, max_size=512):
        self.max_size = max_size
        self.chunks = []
    
    def add_content(self, content, meta):
        current = []
        current_len = 0
        for part in content.split('\n'):
            part_len = len(part)
            if current_len + part_len > self.max_size:
                self.chunks.append({'text': '\n'.join(current), 'meta': meta})
                current = []
                current_len = 0
            current.append(part)
            current_len += part_len
        if current:
            self.chunks.append({'text': '\n'.join(current), 'meta': meta})