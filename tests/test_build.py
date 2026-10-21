import json,tempfile,unittest
from pathlib import Path
from artbook.build import build
class BuildTests(unittest.TestCase):
 def test_escape_copy_and_exclusion(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);(root/'art.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg"/>')
   data={'schema':1,'title':'<script>bad</script>','chapters':[{'title':'A','items':[{'id':'one','title':'A & B','image':'art.svg'},{'id':'skip','title':'hidden','image':'absent','include':False}]}]}
   (root/'c.json').write_text(json.dumps(data));self.assertEqual(build(root/'c.json',root/'out'),1)
   result=(root/'out/index.html').read_text();self.assertNotIn('<script>bad',result);self.assertIn('&lt;script&gt;',result)
   records=json.loads((root/'out/provenance.json').read_text());self.assertEqual(len(records),1);self.assertTrue((root/'out'/records[0]['file']).is_file())
