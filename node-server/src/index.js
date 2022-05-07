const express = require("express");
const multer = require("multer");
const path = require("path");

//DB-CONNECTION
const { MongoClient } = require("mongodb");
// const uri = "mongodb://mongodb:27017/";
const uri = "mongodb://127.0.0.1:27017";
const client = new MongoClient(uri);
const { exec } = require("child_process");

async function connectToDb() {
  try {
    await client.connect();
    console.log("Connected successfully to DataBase");
  } catch (e) {
    console.log("Error");
    console.log(e);
  }
}
connectToDb();
//DB-CONNECTION

const app = express();
const port = 3000;

// const publicPath = path.join(__dirname, "..", "public");
const publicPath = path.join("/home/pj/Documents/ml-project/html-client/");
app.use(express.static(publicPath));

const uploadPath = path.join(__dirname, "..", "uploads");
// const uploadPath = path.join(__dirname, "..", "uploads");
const upload = multer({
  dest: uploadPath,
  fileFilter: function fileFilter(req, file, cb) {
    const ext = path.extname(file.originalname);
    if (ext !== ".csv") {
      return cb(null, false);
    }
    cb(null, true);
  },
  limits: {
    // 1 MB LIMIT
    fileSize: 1024 * 1024,
  },
});

// const pythonCodeDir = "/home/app/python-related/";
const pythonCodeDir = "/home/pj/Documents/ml-project/python-related";
const pythonScript = "script_apriori.py";
// const pathToDataset = "/home/app/node-server/uploads/";
const pathToDataset = "./uploads/";
const minSupport = "0.05";

app.post("/upload", upload.single("csvdata"), function (req, res, next) {
  if (req.file) {
    exec(
      `python3 ${pythonCodeDir}${pythonScript} ${pathToDataset}${req.file.filename} ${req.file.filename} ${minSupport}`
    );
    res.redirect(`http://${req.get("host")}/?msg=upload sucess&id=${req.file.filename}`);
  } else {
    res.redirect(`http://${req.get("host")}/?msg=wrong format`);
  }
});

app.get("/result/:rid", (req, res) => {
  client
    .db("userdatassv")
    .collection("apriori_results")
    .find({ _id: req.params.rid.toString() })
    .toArray((error, result) => {
      if (error) {
        return res.status(500).send(error);
      }
      res.send(result);
    });
});

app.listen(port, () => {
  console.log(`Running on Port ${port}`);
});
