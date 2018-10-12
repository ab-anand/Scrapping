<?php

namespace App\Command;

use Symfony\Component\Console\Output\OutputInterface;

class ResizeImage
{
    /** @var string */
    private $name;

    /** @var int */
    private $width;

    /** @var int */
    private $height;

    /** @var OutputInterface|null */
    private $output;

    /**
     * @param string $name
     * @param int $width
     * @param int $height
     * @param OutputInterface $output
     */
    public function __construct(string $name, int $width, int $height, ?OutputInterface &$output = null)
    {
        $this->name = $name;
        $this->width = $width;
        $this->height = $height;
        $this->output = $output;
    }

    /**
     * @return string
     */
    public function getName(): string
    {
        return $this->name;
    }

    /**
     * @return int
     */
    public function getWidth(): int
    {
        return $this->width;
    }

    /**
     * @return int
     */
    public function getHeight(): int
    {
        return $this->height;
    }

    /**
     * @return OutputInterface|null
     */
    public function getOutput(): ?OutputInterface
    {
        return $this->output;
    }
}