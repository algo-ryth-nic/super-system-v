const express = require('express')
const multer = require('multer')
const path = require('path')


const app = express()
const port = 3000

const publicPath = path.join(__dirname, '..', 'public');
app.use(express.static(publicPath))

const uploadPath = path.join(__dirname, '..', 'uploads');
const upload = multer({
  dest: uploadPath,
  fileFilter: function fileFilter(req, file, cb) {
    const ext = path.extname(file.originalname);
    if (ext !== '.csv') {
      return cb(null, false)
    }
    cb(null, true)
  },
  limits: {
    // 1 MB LIMIT
    fileSize: 1024 * 1024
  }
})


app.post('/upload', upload.single('csvdata'), function (req, res, next) {
  if (req.file) {
    res.redirect(`http://${req.get('host')}/?msg=upload sucess&id=${req.file.filename}`);
  }
  else {
    res.redirect(`http://${req.get('host')}/?msg=wrong format`);
  }
})


app.listen(port, () => {
  console.log(`Running on Port ${port}`)
})
