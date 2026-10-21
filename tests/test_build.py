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
 def test_pixel_grid_metadata_required(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);(root/'art.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg"/>')
   item={'id':'pixel','title':'Pixels','image':'art.svg','pixel':True}
   data={'schema':1,'title':'Test','chapters':[{'title':'A','items':[item]}]}
   (root/'c.json').write_text(json.dumps(data))
   with self.assertRaises(ValueError):build(root/'c.json',root/'out')
   item['grid']={'native_size':[96,96],'cell_size':[48,48],'anchor':[24,24]}
   (root/'c.json').write_text(json.dumps(data));build(root/'c.json',root/'out')
   self.assertIn('data-grid=',(root/'out/index.html').read_text())
   self.assertTrue((root/'out/pixel-grid.js').is_file())
