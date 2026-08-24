// ============================================================
// API URL
// ============================================================

const API_URL = "http://127.0.0.1:8000";


// ============================================================
// UPLOAD DOCUMENT
// ============================================================

async function uploadDocument() {

    const fileInput = document.getElementById("fileInput");
    const uploadStatus = document.getElementById("uploadStatus");
    const uploadButton = document.getElementById("uploadButton");

    // Check if file selected

    if (!fileInput.files.length) {

        uploadStatus.innerHTML =
            `<div class="error">
                Please select a PDF or TXT file.
            </div>`;

        return;
    }


    const file = fileInput.files[0];

    // Check extension

    const fileName = file.name.toLowerCase();

    if (
        !fileName.endsWith(".pdf") &&
        !fileName.endsWith(".txt")
    ) {

        uploadStatus.innerHTML =
            `<div class="error">
                Only PDF and TXT files are allowed.
            </div>`;

        return;
    }


    // Create FormData

    const formData = new FormData();

    formData.append("file", file);


    // Disable button

    uploadButton.disabled = true;

    uploadButton.innerText = "Processing...";


    uploadStatus.innerHTML =
        `<div class="loading">
            📄 Uploading and processing document...
        </div>`;


    try {

        const response = await fetch(
            `${API_URL}/upload`,
            {
                method: "POST",
                body: formData
            }
        );


        const data = await response.json();


        if (data.success) {

            uploadStatus.innerHTML =
                `<div class="success">

                    ✅ Document uploaded successfully!

                    <br><br>

                    <strong>File:</strong>
                    ${escapeHTML(data.filename)}

                    <br>

                    <strong>Chunks created:</strong>
                    ${data.chunks}

                </div>`;

            document.getElementById("answer").innerText =
                "Document is ready. Ask a question!";

        }
        else {

            uploadStatus.innerHTML =
                `<div class="error">
                    ❌ ${escapeHTML(data.message)}
                </div>`;

        }


    }
    catch (error) {

        console.error(error);

        uploadStatus.innerHTML =
            `<div class="error">

                ❌ Could not connect to the backend.

                <br><br>

                Make sure FastAPI is running on:

                <br>

                http://127.0.0.1:8000

            </div>`;

    }


    // Enable button again

    uploadButton.disabled = false;

    uploadButton.innerText = "Upload Document";

}



// ============================================================
// ASK QUESTION
// ============================================================

async function askQuestion() {

    const questionInput =
        document.getElementById("questionInput");

    const answerBox =
        document.getElementById("answer");

    const sourcesBox =
        document.getElementById("sources");

    const askButton =
        document.getElementById("askButton");


    const question =
        questionInput.value.trim();


    // Check question

    if (!question) {

        answerBox.innerHTML =
            `<div class="error">
                Please enter a question.
            </div>`;

        return;
    }


    // Disable button

    askButton.disabled = true;

    askButton.innerText = "Thinking...";


    answerBox.innerHTML =
        `<div class="loading">
            🤔 Searching the document...
        </div>`;


    sourcesBox.innerHTML =
        `<div class="loading">
            Searching relevant chunks...
        </div>`;


    try {

        const response = await fetch(
            `${API_URL}/ask`,
            {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    question: question
                })

            }
        );


        const data = await response.json();


        console.log("Backend response:", data);


        // ====================================================
        // ANSWER
        // ====================================================

        if (data.success) {

            answerBox.innerText =
                data.answer || "No answer found.";

        }
        else {

            answerBox.innerText =
                data.answer || "Something went wrong.";

        }


        // ====================================================
        // SOURCES
        // ====================================================

        displaySources(data.sources);


    }
    catch (error) {

        console.error(error);

        answerBox.innerHTML =
            `<div class="error">

                ❌ Error connecting to backend.

                <br><br>

                ${escapeHTML(error.message)}

            </div>`;


        sourcesBox.innerHTML =
            `<div class="error">
                Could not retrieve context.
            </div>`;

    }


    // Enable button

    askButton.disabled = false;

    askButton.innerText = "Ask Question";

}



// ============================================================
// DISPLAY SOURCES
// ============================================================

function displaySources(sources) {

    const sourcesBox =
        document.getElementById("sources");


    // No sources

    if (
        !sources ||
        !Array.isArray(sources) ||
        sources.length === 0
    ) {

        sourcesBox.innerHTML =
            `<p class="empty-message">
                No retrieved context found.
            </p>`;

        return;
    }


    // Clear previous sources

    sourcesBox.innerHTML = "";


    // Loop through chunks

    sources.forEach(
        (source, index) => {

            const sourceCard =
                document.createElement("div");

            sourceCard.className = "source-card";


            // ------------------------------------------------
            // FIX FOR [object Object]
            // ------------------------------------------------

            let text = "";


            if (typeof source === "string") {

                // Backend returned a normal string

                text = source;

            }

            else if (
                typeof source === "object" &&
                source !== null
            ) {

                // Backend returned an object

                if (source.text) {

                    text = source.text;

                }

                else if (source.content) {

                    text = source.content;

                }

                else if (source.chunk) {

                    text = source.chunk;

                }

                else if (source.page_content) {

                    text = source.page_content;

                }

                else {

                    // Last resort:
                    // convert object into readable JSON

                    text = JSON.stringify(
                        source,
                        null,
                        2
                    );

                }

            }

            else {

                text = String(source);

            }


            // ------------------------------------------------
            // Display
            // ------------------------------------------------

            sourceCard.innerHTML = `

                <h3>
                    Chunk ${index + 1}
                </h3>

                <p>
                    ${escapeHTML(text)}
                </p>

            `;


            sourcesBox.appendChild(
                sourceCard
            );

        }
    );

}



// ============================================================
// HTML ESCAPE
// ============================================================

function escapeHTML(text) {

    if (text === null || text === undefined) {

        return "";

    }


    return String(text)

        .replace(/&/g, "&amp;")

        .replace(/</g, "&lt;")

        .replace(/>/g, "&gt;")

        .replace(/"/g, "&quot;")

        .replace(/'/g, "&#039;");

}