const fs = require("fs");
const path = require("path");

const files = fs
  .readdirSync(path.join(root, "projects/rikxiniao/app/assets"), { withFileTypes: true })
  .filter((e) => e.isFile() && e.name.endsWith(".js"))
  .map((e) => path.join("projects/rikxiniao/app/assets", e.name));
const bundle = path.join(root, "projects/rikxiniao/app/bundle.js");
if (fs.existsSync(bundle)) files.push("projects/rikxiniao/app/bundle.js");

const root = path.resolve(__dirname, "..");

const petSettingsPatterns = [
  {
    old:
      "className: `input-field pet-name-input`, value: g7.name, onChange: (e97) => _7({ name: e97.target.value }), maxLength: 12",
    new:
      "className: `input-field pet-name-input`, value: g7.name, onChange: (e97) => _7({ name: e97.target.value }), onKeyDown: (e97) => { if (e97.key === `Enter`) { e97.preventDefault(); y7 && v7(); } }, maxLength: 12",
  },
  {
    old:
      "className:`input-field pet-name-input`,value:g.name,onChange:e=>_({name:e.target.value}),maxLength:12",
    new:
      "className:`input-field pet-name-input`,value:g.name,onChange:e=>_({name:e.target.value}),onKeyDown:e=>{if(e.key===`Enter`){e.preventDefault();y&&v();}},maxLength:12",
  },
];

const onboardingPatterns = [
  {
    old:
      "className: `input-field`, maxLength: 12, value: Ke5, onChange: (e97) => Je5(e97.target.value)",
    new:
      "className: `input-field`, maxLength: 12, value: Ke5, onChange: (e97) => Je5(e97.target.value), onKeyDown: (e97) => { if (e97.key === `Enter`) { e97.preventDefault(); wt4(); } }",
  },
  {
    old:
      "className:`input-field`,maxLength:12,value:Ke,onChange:e=>Je(e.target.value)",
    new:
      "className:`input-field`,maxLength:12,value:Ke,onChange:e=>Je(e.target.value),onKeyDown:e=>{if(e.key===`Enter`){e.preventDefault();wt();}}",
  },
];

for (const rel of files) {
  const file = path.join(root, rel);
  let text = fs.readFileSync(file, "utf8");
  let changed = false;

  for (const { old, new: replacement } of petSettingsPatterns) {
    if (text.includes(old)) {
      text = text.replace(old, replacement);
      console.log(rel, "pet settings patched");
      changed = true;
      break;
    }
  }

  for (const { old, new: replacement } of onboardingPatterns) {
    if (text.includes(old)) {
      text = text.replace(old, replacement);
      console.log(rel, "onboarding patched");
      changed = true;
      break;
    }
  }

  if (changed) fs.writeFileSync(file, text, "utf8");
}
