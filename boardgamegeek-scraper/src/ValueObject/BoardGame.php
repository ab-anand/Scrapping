<?php

namespace App\ValueObject;

use SimpleXMLElement;

class BoardGame
{
    /** @var int */
    private $id;

    /** @var string */
    private $name;

    /** @var string */
    private $description;

    /** @var null|string */
    private $image;

    /**
     * @param int $id
     * @param string $name
     * @param string $description
     * @param null|string $image
     */
    public function __construct(
        int $id,
        string $name,
        string $description,
        ?string $image
    ) {
        $this->id = $id;
        $this->name = $name;
        $this->description = $description;
        $this->image = $image;
    }

    /**
     * @return int
     */
    public function getId(): int
    {
        return $this->id;
    }

    /**
     * @return string
     */
    public function getName(): string
    {
        return htmlspecialchars_decode($this->name);
    }

    /**
     * @return string
     */
    public function getDescription(): string
    {
        return htmlspecialchars_decode($this->description);
    }

    /**
     * @return null|string
     */
    public function getImage(): ?string
    {
        return $this->image;
    }

    /**
     * @return SimpleXMLElement
     */
    public function toXML(): SimpleXMLElement
    {
        $xmlstr = <<<XML
<?xml version='1.0' standalone='yes'?>
<boardgames>
    <boardgame>
        <id>{$this->getId()}</id>
        <name><![CDATA[{$this->getName()}]]></name>
        <description><![CDATA[{$this->getDescription()}]]></description>
        <image>{$this->getImage()}</image>
    </boardgame>
</boardgames>
XML;

        return new SimpleXMLElement($xmlstr);
    }
}
