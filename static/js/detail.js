async function copyTransactionId() {
  const transactionId = document.getElementById("id_transaction").textContent;
  const copyButton = document.getElementById("copyButton");
  const copyFeedback = document.getElementById("copyFeedback");
  console.log(transactionId);
  try {
    await navigator.clipboard.writeText(transactionId);

    copyButton.innerHTML = '<i data-lucide="check" class="h-4 w-4"></i>';
    copyButton.classList.remove("text-gray-400", "hover:text-blue-600");
    copyButton.classList.add("text-green-600");

    copyFeedback.classList.remove("hidden");

    setTimeout(() => {
      copyButton.innerHTML = '<i data-lucide="copy" class="h-4 w-4"></i>';
      copyButton.classList.remove("text-green-600");
      copyButton.classList.add("text-gray-400", "hover:text-blue-600");
      copyFeedback.classList.add("hidden");

      lucide.createIcons();
    }, 2000);

    lucide.createIcons();
  } catch (err) {
    console.error("Erro ao copiar: ", err);

    // Fallback to older browsers or when the API failure
    const textArea = document.createElement("textarea");
    textArea.value = transactionId;
    textArea.style.position = "fixed";
    textArea.style.left = "-999999px";
    textArea.style.top = "-999999px";
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();

    try {
      document.execCommand("copy");
      copyFeedback.classList.remove("hidden");
      setTimeout(() => {
        copyFeedback.classList.add("hidden");
      }, 2000);
    } catch (fallbackErr) {
      console.error("Fallback também falhou: ", fallbackErr);
      alert(
        "Não foi possível copiar automaticamente. Por favor, selecione e copie manualmente."
      );
    } finally {
      document.body.removeChild(textArea);
    }
  }
}
