console.log("Hello World");

const url = new URL(window.location.href);
console.log(url);

const getResult = async (id) => {
  const result = await fetch(`http://${url.host}/result/${id}`);
  const resultObj = await result.json();
  console.log(resultObj);
  return resultObj;
};

const plotData = (obj) => {
  const body = document.querySelector("body");
  body.innerHTML = "";
  body.style.overflow = "auto";
  body.style.padding = "2rem";
  body.style.height = "100%";
  body.style.flexDirection = "column";

  const rules = JSON.parse(obj["association-rules"]);
  let str = "";
  rules.slice(0, 20).forEach((rule, index) => {
    const ruleStr = `${rule["antecedents"]} → ${rule["consequents"].join(", ")}`;

    str += `
        <div class="card animate-slidein" style="animation-delay: ${index * 100}ms" id="${index}">
        <div class="card-body">
        <div class="card-title">${ruleStr}</div>
          <p class="card-text">
            When <strong>${rule["consequents"].join(", ")}</strong> ${
      rule["consequents"].length > 1 ? "are" : "is"
    } bought then <strong>${rule["antecedents"]}</strong> ${rule["antecedents"].length > 1 ? "are" : "is"} ${rule[
      "lift"
    ].toFixed(2)} times more likely to be bought.        
          </p>
          <span class="badge badge-dark">Occurs: ${(rule["support"] * 100).toFixed(2)}%</span>
          <span class="badge badge-success">Confidence: ${(rule["confidence"] * 100).toFixed(2)}%</span>
        </div>
        </div>
        `;
  });

  const table = `
    <h5>Recommendations Generated <span class="badge badge-secondary">${rules.length}</span></h5>
    <div class="messages-container">
        ${str}
        <a href="#" id="see-all">See All</a>
    </div>
      `;
  body.innerHTML = table;

  const seeAllBtn = document.getElementById("see-all");
  seeAllBtn.addEventListener("click", () => {
    alert("Please upgrade to a paid account!");
  });
};

const plotDataHandler = async () => {
  const obj = await getResult(url.searchParams.get("id"));
  if (obj.length == 0) {
    // check for results in every 5 seconds
    setTimeout(plotDataHandler, 5 * 1000);
  } else {
    // document.getElementById("spinner").innerHTML = "DATA PROCESSING COMPLETE";
    // plots the data
    plotData(obj[0]);
  }
};

// on upload redirect
if (url.searchParams.get("id")) {
  const contentBox = document.querySelector(".menu-content-container");
  contentBox.innerHTML = `</div>
${
  url.searchParams.get("id")
    ? `     <div class="spinner-container">
          <div class="spinner-border"></div>
          <strong>Processing...</strong>
        </div>`
    : "Error"
}`;
  plotDataHandler();
}

// file upload & drag and drop related
if (!url.search) {
  const dropZone = document.querySelector("#drop-zone");

  dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    console.log("file is in drop zone");
    if (e.dataTransfer.types.indexOf("Files")) {
      dropZone.classList.add("active");
    }
  });

  dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("active");
  });

  dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    console.log("File(s) dropped");

    if (e.dataTransfer.items) {
      // Using DataTransferItemList interface to access the file(s)
      console.log(e.dataTransfer.items[0]);
      // If dropped item is a file
      if (e.dataTransfer.items[0].kind === "file") {
        const file = e.dataTransfer.items[0].getAsFile();
        console.log("file[" + i + "].name = " + file.name);
        validateFile(file) ? document.querySelector("form").submit() : console.log("invalid file");
      }
    }
  });

  document.querySelector("input[type=file]").addEventListener("change", (e) => {
    console.log(e.target.files[0]);
    const file = e.target.files[0];
    validateFile(file) ? document.querySelector("form").submit() : console.log("invalid file");
  });

  document.querySelector("#browse-button").addEventListener("click", () => {
    document.getElementById("file").click();
  });

  function validateFile(file) {
    // file type validation
    if (file.type !== "text/csv" && file.type !== "application/vnd.ms-excel") {
      alert("Please upload a csv file or an excel file");
      return false;
    }
    // file size validation
    if (file.size > 10 ** 6) {
      alert("Please upload a file less than 1 MB");
      return false;
    }
    return true;
  }
}
