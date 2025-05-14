import yaml
from pathlib import Path

class Settings:
    def __init__(self):
        config_path = Path(__file__).parent / "config.yaml"
        with open(config_path, encoding='utf-8') as f:
            self._config = yaml.safe_load(f)
        
        # 将路径校验移到__init__内部
        upload_dir = Path(self._config.get("web", {}).get("upload_dir", "uploads"))
        if not upload_dir.exists():
            upload_dir.mkdir(parents=True)

    def __getattr__(self, name):
        value = self._config.get(name, {})
        if isinstance(value, dict):  # 递归处理嵌套配置
            return type('Settings', (object,), {
                '__getattr__': lambda _, key: value.get(key, None)
            })()
        return value

settings = Settings()