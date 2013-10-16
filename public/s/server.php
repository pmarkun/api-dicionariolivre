<?php
  header('Access-Control-Allow-Origin: *');
  require_once('settings.php');
  require_once('lib/recaptchalib.php');
  $resp = recaptcha_check_answer ($SETTINGS["RECAPTCHA_KEY"],
                                $_SERVER["REMOTE_ADDR"],
                                $_POST["recaptcha_challenge_field"],
                                $_POST["recaptcha_response_field"]);

  if (!$resp->is_valid) {
    // What happens when the CAPTCHA was entered incorrectly
    die ("The reCAPTCHA wasn't entered correctly. Go back and try it again." .
         "(reCAPTCHA said: " . $resp->error . ")");
  } else {
    $url = $SETTINGS['SERVER'] . $_POST['colecoes'] . "/verbete/" . $_POST['id'] ."/";
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_HEADER, 0);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($_POST["palavra"]));
    curl_exec($ch);
    curl_close($ch);
  }
?>