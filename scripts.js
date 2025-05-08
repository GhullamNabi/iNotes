// Add this in the <head> section to handle the dynamic post content modification
    function processPostContent() {
      // Get all post content
      var postContent = document.querySelector('.post-body');
      if (!postContent) return;

      // Detect 'code:' in the content and handle it
      var content = postContent.innerHTML;
      var codeStartIndex = content.indexOf('code:');

      if (codeStartIndex !== -1) {
        // Extract everything after 'code:'
        var codeContent = content.substring(codeStartIndex + 5).trim();

        // Create the code block
        var codeBlock = `<div class="code-container">
                           <button class="copy-btn" onclick="copyCode()">Copy Code</button>
                           <div class="code-card">${codeContent}</div>
                         </div>`;

        // Replace the content with code block and other text
        postContent.innerHTML = content.substring(0, codeStartIndex) + codeBlock;
      }
    }

    function copyCode() {
      // Copy the code to clipboard
      const codeBlock = document.querySelector('.code-card');
      if (!codeBlock) return;
      
      const range = document.createRange();
      range.selectNodeContents(codeBlock);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      try {
        document.execCommand('copy');
        alert("Code copied to clipboard!");
      } catch (err) {
        alert("Failed to copy!");
      }
      selection.removeAllRanges();
    }

    // Call the function once the page is loaded
    window.onload = processPostContent;
