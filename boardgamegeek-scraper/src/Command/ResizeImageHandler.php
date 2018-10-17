<?php

namespace App\Command;

use Gumlet\ImageResize;
use Gumlet\ImageResizeException;
use Symfony\Component\Console\Output\OutputInterface;

class ResizeImageHandler
{
    /** @var string */
    private $rootDir;

    /**
     * @param string $rootDir
     */
    public function __construct(string $rootDir)
    {
        $this->rootDir = $rootDir;
    }

    /**
     * @param ResizeImage $resizeImage
     *
     * @throws ImageResizeException
     */
    public function handle(ResizeImage $resizeImage): void
    {
        $directories = scandir($this->rootDir . '/../public/boardgames/');
        array_walk($directories, function($directory) {
            return intval($directory);
        });
        sort($directories);

        $name = $resizeImage->getName();
        $height = $resizeImage->getHeight();
        $width = $resizeImage->getWidth();

        foreach ($directories as $key => $directory) {
            if (!is_dir($this->rootDir . '/../public/boardgames/' . $directory)) {
                unset($directories[$key]);
                continue;
            }

            if (!file_exists($this->rootDir . '/../public/boardgames/' . $directory . '/image.jpg') &&
                !file_exists($this->rootDir . '/../public/boardgames/' . $directory . '/image.png')
            ) {
                unset($directories[$key]);
                continue;
            }

            $sourceImage = $this->rootDir . '/../public/boardgames/' . $directory . '/image.jpg';
            if (file_exists($this->rootDir . '/../public/boardgames/' . $directory . '/image.png')) {
                $sourceImage = $this->rootDir . '/../public/boardgames/' . $directory . '/image.png';
            }

            $this->resizeImage(
                $sourceImage,
                $name,
                $height,
                $width
            );

            if ($resizeImage->getOutput() instanceof OutputInterface) {
                $resizeImage->getOutput()->writeln("<info>Resized image in $directory</info>");
            }
            unset($directories[$key]);
        }
    }

    /**
     * @param string $sourceImage
     * @param string $name
     * @param int $width
     * @param int $heigth
     *
     * @throws ImageResizeException
     */
    private function resizeImage(
        string $sourceImage,
        string $name,
        int $width,
        int $heigth
    ): void {
        $extension = array_reverse(explode('.', $sourceImage))[0];
        $destination = dirname($sourceImage) . '/' . $name . '.' . $extension;

        if (file_exists($destination)) {
            return;
        }

        $image = new ImageResize($sourceImage);
        $image->resizeToBestFit($width, $heigth);
        $image->save($destination);

        unset($image);
    }
}