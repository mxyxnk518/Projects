const express = require("express");
const app = express();
const fileUpload = require('express-fileupload');
const port = 3000;
const bodyParser = require('body-parser');

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
    extended: true
}));
app.engine('html', require('ejs').renderFile);
app.set('view engine', 'html');

app.use(fileUpload());
app.use("/uploads", express.static(__dirname + "/uploads"));

const { GoogleGenerativeAI } = require("@google/generative-ai");
const fs = require("fs");


// Access your API key as an environment variable (see "Set up your API key" above)
const genAI = new GoogleGenerativeAI("AIzaSyAzsqBT9wCN03wqE3T3FtbfI11Pe1W71H0");

function fileToGenerativePart(path, mimeType) {
    return {
        inlineData: {
            data: Buffer.from(fs.readFileSync(path)).toString("base64"),
            mimeType
        },
    };
}

async function run(path, type, message) {
    // For text-and-image input (multimodal), use the gemini-pro-vision model
    const model = genAI.getGenerativeModel({ model: "gemini-pro-vision" });

    const prompt = message;

    const imageParts = [
        fileToGenerativePart(path, type)
    ];

    const result = await model.generateContent([prompt, ...imageParts]);
    const response = await result.response;
    const text = response.text();
    return text
}



app.get("/", (req, res) => {
    res.render(__dirname + '/templates/home.html')
})

app.get("/assignments/:id", (req, res) => {
    const id = req.params.id;
    res.render(__dirname + "/templates/positioning.html", { "task": "reading", "id": id, "error": "" })
})


app.post("/assignments/:id", async (req, res) => {
    const id = req.params.id;
    let task = req.body.task
    let filename;
    let uploadPath;
    if (req.files) {
        filename = req.files.file;
        uploadPath = __dirname + '/uploads/' + filename.name;
        filename.mv(uploadPath, (err) => {
            if (err) throw err;
        })
    }

    let type = uploadPath.split(".")

    type = type[type.length - 1]

    console.log(uploadPath);

    if (type == "jpg") {
        type = "jpeg"
    }

    let response

    let prompt

    if (task == "reading") {
        prompt = `Is the person looking at the computer? strictly return yes, no or not sure`
    } else {
        prompt = `Is the person ${task}? strictly return yes, no or not sure`
    }

    setTimeout(async () => {
        response = await run(uploadPath, `image/${type}`, prompt)

        if (response.includes("yes")) {
            res.redirect("http://localhost:5500/face-api/")
        } else {
            res.render(__dirname + "/templates/assignment-load.html", { "task": task, "id": id, "error": "Position is not suitable for task." })
        }

    }, 2000)

})


app.listen(port, () => {
    console.log(`Server is running on ${port}`);
})
