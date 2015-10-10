<?php

//    seed-node-monitor: a monitor system for cryptocurrency seed nodes
//    Copyright (C) 2015  Myckel Habets
//
//    This program is free software: you can redistribute it and/or modify
//    it under the terms of the GNU Affero General Public License as published
//    by the Free Software Foundation, either version 3 of the License, or
//    (at your option) any later version.
//
//    This program is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU Affero General Public License for more details.
//
//    You should have received a copy of the GNU Affero General Public License
//    along with this program.  If not, see <http://www.gnu.org/licenses/>.



slack_send($message)
    {
    $slack_webhook_url = "";
    $ch = curl_init($slack_webhook_url);

    $msg_str = array("text" => $message, "username" => "Seed-node-bot", "icon_emoji" => ":satellite:");
    $json_data = json_encode($msg_str);

    $data = array('payload' => $json_data);

    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);

    curl_exec($ch);
    curl_close($ch);
    }



?>