<?php

require 'vendor/autoload.php';

use Aws\Sns\Message;
use Aws\Sns\MessageValidator;
use Aws\ElasticsearchService\ElasticsearchPhpHandler;
use Elasticsearch\ClientBuilder;
use Aws\Credentials\CredentialProvider;
use Aws\Credentials\Credentials;

// Create a handler (with the region of your Amazon Elasticsearch Service domain)
$provider = CredentialProvider::fromCredentials(
    new Credentials('KEY', 'SecretKEY')
);
$handler = new ElasticsearchPhpHandler('us-west-2');

// Use this handler to create an Elasticsearch-PHP client
$client = ClientBuilder::create()
    ->setHandler(new ElasticsearchPhpHandler('us-west-2'))
    ->setHosts(['https://search-twittermap-zhychepoqowvbu7g3v5r7uqesq.us-west-2.es.amazonaws.com:443'])
    ->build();

 // Make sure the request is POST
 if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
     http_response_code(405);
     die;
 }

try {
    // Create a message from the post data and validate its signature
    $message = Message::fromRawPostData();
    $validator = new MessageValidator();
    $validator->validate($message);
} catch (Exception $e) {
    // Pretend we're not here if the message is invalid
    http_response_code(404);
    die;
}

if ($message['Type'] === 'SubscriptionConfirmation') {
    file_get_contents($message['SubscribeURL']);
    http_response_code(200);

} elseif ($message['Type'] === 'Notification') {
    // Do something with the notification
    $tweetMsg = json_decode($message['Message'], true);
    // Use the client as you normally would
    $params = [
        'index' => 'tweetmap',
        'type' => 'tweets',
        'body' => $tweetMsg
    ];
    $client->index($params);
    http_response_code(200);
}
