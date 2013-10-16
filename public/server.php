<?php
  header('Access-Control-Allow-Origin: *');
  require_once('lib/recaptchalib.php');
  $privatekey = "6LeJ2egSAAAAAI4mw6MMSQbCC8aWQsYIQzq1HF4e";
  $resp = recaptcha_check_answer ($privatekey,
                                $_SERVER["REMOTE_ADDR"],
                                $_POST["recaptcha_challenge_field"],
                                $_POST["recaptcha_response_field"]);

  if (!$resp->is_valid) {
    // What happens when the CAPTCHA was entered incorrectly
    die ("The reCAPTCHA wasn't entered correctly. Go back and try it again." .
         "(reCAPTCHA said: " . $resp->error . ")");
  } else {
    echo "Aloha!";
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, "http://0.0.0.0/error");
    curl_setopt($ch, CURLOPT_HEADER, 0);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $_POST["palavra"]);
    curl_exec($ch);
    curl_close($ch);
  }
?>