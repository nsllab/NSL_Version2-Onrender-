<?php
// popup.php
session_start();

// Check if the user has chosen to hide the popup for today
$should_show = true;
if (isset($_COOKIE['hide_popup'])) {
    $hide_until = $_COOKIE['hide_popup'];
    if (strtotime($hide_until) > time()) {
        $should_show = false;
    }
}

if ($should_show) {
    ?>
    <!-- Modal HTML -->
    <div id="welcomeModal" class="modal">
        <div class="modal-content">
            <span class="close">&times;</span>
            <img src="popupz.jpg" alt="Welcome Banner" style="width: 100%; max-width: 600px;">
            <div class="modal-footer">
                <label>
                    <input type="checkbox" id="dontShowToday"> Don't show this message today
                </label>
                <button onclick="closeModal()">Close</button>
            </div>
        </div>
    </div>

    <!-- CSS Styles -->
    <style>
    .modal {
        display: none;
        position: fixed;
        z-index: 1000;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0,0,0,0.5);
    }

    .modal-content {
        background-color: #fefefe;
        margin: 15% auto;
        padding: 20px;
        border: 1px solid #888;
        width: 80%;
        max-width: 600px;
        border-radius: 5px;
        position: relative;
    }

    .close {
        color: #aaa;
        float: right;
        font-size: 28px;
        font-weight: bold;
        cursor: pointer;
    }

    .close:hover,
    .close:focus {
        color: black;
        text-decoration: none;
        cursor: pointer;
    }

    .modal-footer {
        margin-top: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .modal-footer button {
        padding: 8px 16px;
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }

    .modal-footer button:hover {
        background-color: #45a049;
    }
    </style>

    <!-- JavaScript -->
    <script>
    window.onload = function() {
        var modal = document.getElementById('welcomeModal');
        modal.style.display = "block";
    }

    function closeModal() {
        var modal = document.getElementById('welcomeModal');
        var checkbox = document.getElementById('dontShowToday');
        
        if (checkbox.checked) {
            // Set cookie to expire at the end of the current day
            var now = new Date();
            var midnight = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1, 0, 0, 0);
            document.cookie = "hide_popup=" + midnight.toUTCString() + "; path=/";
        }
        
        modal.style.display = "none";
    }

    // Close when clicking the X
    document.getElementsByClassName('close')[0].onclick = function() {
        closeModal();
    }

    // Close when clicking outside the modal
    window.onclick = function(event) {
        var modal = document.getElementById('welcomeModal');
        if (event.target == modal) {
            closeModal();
        }
    }
    </script>
    <?php
}
?>