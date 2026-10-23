"""Copy canonical lesson Markdown into the static site's offline/network fallback."""
import json,shutil
from pathlib import Path
root=Path(__file__).resolve().parents[1]
for data in (root/'docs/units').glob('data-*.js'):
 text=data.read_text();lessons=json.loads(text[text.index('concat(')+7:text.rindex(']')+1])
 for lesson in lessons:
  source=root/'units'/lesson['markdown'];target=root/'docs/units/content'/lesson['markdown']
  target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
print('Published original Markdown lessons.')
