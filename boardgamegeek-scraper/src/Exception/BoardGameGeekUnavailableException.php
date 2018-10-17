<?php

namespace App\Exception;

use Exception;

class BoardGameGeekUnavailableException extends Exception
{
    /**
     * @return BoardGameGeekUnavailableException
     */
    public static function create(): self
    {
        return new self('BoardGameGeek is unavailable, please wait a minute.');
    }
}
