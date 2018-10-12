<?php

namespace App\Command\Console;

use App\Command\GetBGGData;
use App\Command\GetBGGDataHandler;
use App\Command\ResizeImage;
use App\Command\ResizeImageHandler;
use Exception;
use Gumlet\ImageResizeException;
use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputArgument;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;

class ResizeImages extends Command
{
    /** @var ResizeImageHandler */
    private $resizeImageHandler;

    /**
     * @param ResizeImageHandler $resizeImageHandler
     * @param null $name
     */
    public function __construct(ResizeImageHandler $resizeImageHandler, $name = null)
    {
        parent::__construct($name);

        $this->resizeImageHandler = $resizeImageHandler;
    }

    protected function configure()
    {
        $this
            ->setName('app:resize-images')
            ->setDescription('Resizes all boardgame images')
            ->addArgument('name', InputArgument::OPTIONAL, 'The name for the new images', 'thumbnail')
            ->addArgument('width', InputArgument::OPTIONAL, 'The width for the new images', 250)
            ->addArgument('length', InputArgument::OPTIONAL, 'The length for the new images', 250);
    }

    /**
     * @param InputInterface $input
     * @param OutputInterface $output
     *
     * @return int|null|void
     *
     * @throws ImageResizeException
     */
    protected function execute(InputInterface $input, OutputInterface $output)
    {
        ini_set('memory_limit', '3G');

        $output->writeln([
            'Resizing Images',
            '===============',
            '',
        ]);

        $this->resizeImageHandler->handle(
            new ResizeImage(
                $input->getArgument('name'),
                $input->getArgument('width'),
                $input->getArgument('length'),
                $output
            )
        );
    }
}
