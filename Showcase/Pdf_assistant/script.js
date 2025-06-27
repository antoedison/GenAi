
const uploadForm = document.getElementById("uploadForm");
const fileInput = document.getElementById("file");
const uploadStatus = document.getElementById("uploadStatus");

uploadForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const file = fileInput.files[0];

  if (!file) {
    uploadStatus.innerHTML = "⚠️ Please select a file.";
    return;
  }

  uploadStatus.innerHTML = "⏳ Uploading...";

  const reader = new FileReader();
  reader.onload = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/Upload_files", {
        method: "POST",
        headers: {
          "Content-Type": "application/pdf",
          "encoded-filename": encodeURIComponent(file.name)
        },
        body: reader.result
      });

      const result = await response.json();

      if (response.ok) {
        uploadStatus.innerHTML = `✅ <strong>${result.message}</strong><br>📌 Chunks Added: ${result.chunks_added}`;
      } else {
        uploadStatus.innerHTML = `❌ Error: ${result.detail}`;
      }
    } catch (err) {
      uploadStatus.innerHTML = `❌ Upload failed: ${err.message}`;
    }
  };
  reader.readAsArrayBuffer(file);
});

// Handle Query Submission
const queryForm = document.getElementById("queryForm");
const questionInput = document.getElementById("question");
const answerOutput = document.getElementById("answerOutput");

queryForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const question = questionInput.value.trim();
  if (!question) {
    answerOutput.innerHTML = "⚠️ Please enter a question.";
    return;
  }

  answerOutput.innerHTML = "⏳ Getting answer...";

  try {
    const response = await fetch(`http://127.0.0.1:8000/answer?query=${encodeURIComponent(question)}`);

    const answer = await response.text();

    if (response.ok) {
      answerOutput.innerHTML = `💡 <strong>Answer:</strong> ${answer}`;
    } else {
      answerOutput.innerHTML = `❌ Error: ${answer}`;
    }
  } catch (err) {
    answerOutput.innerHTML = `❌ Request failed: ${err.message}`;
  }
});