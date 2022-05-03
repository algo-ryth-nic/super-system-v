console.log("Hello World")

const url = new URL(window.location.href);


const msgBox = document.getElementById('msg-box');
msgBox.innerHTML = `
<div class="alert alert-${url.searchParams.get("id") ? "success" : "danger"}" role="alert">
<h3>id: ${url.searchParams.get("id") || "?"}</h3>
${url.searchParams.get("id") ? "Data upload success" : "Data does not exist"}
</div>
${url.searchParams.get("id") ?
        `<div id=\"spinner\" class=\"alert alert-info\" role=\"alert\">
<div class='spinner-border'></div>
Please wait while the data is being processed, You can save the Url to view the results later        
</div>` : ""
    }
`;

const getResult = async (id) => {    
    const result = await fetch(`http://${url.host}/result/${id}`);
    const resultObj = await result.json();
    return resultObj[0];
    
}

const plotData = (obj) => {
    console.log(JSON.parse(obj["frequent_items"]));
    console.log(JSON.parse(obj["association-rules"]));
}

const plotDataHandler = async () => {
    const obj = await getResult(url.searchParams.get("id"));
    if(obj.length == 0){
        // check for results in every 10 seconds if not yet processed
        setTimeout(plotDataHandler, 10 * 1000);
    }
    else{
        document.getElementById('spinner').innerHTML = "DATA PROCESSING COMPLETE";
        plotData(obj[0]);
    }
}

if (url.searchParams.get("id")) {
    document.getElementsByTagName('button')[0].innerHTML = "DATA UPLOADED";
    document.getElementsByTagName('button')[0].disabled = true;
    plotDataHandler();
}

