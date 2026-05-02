# TODO for AI

*   **Wait for user to run `termux-setup-storage`:** The user needs to execute `termux-setup-storage` in their Termux terminal to grant storage access and create necessary symlinks.
*   **Retry getting `/sdcard` folder size:** After the user confirms they have run `termux-setup-storage`, retry calculating the size of `/sdcard` (or `~/storage/shared`).
*   **Generate HTML for `/sdcard` size:** Once the size is successfully obtained, create an HTML file (e.g., `sdcard_size.html`) to display the result and inform the user where to access it.