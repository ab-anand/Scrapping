<?php

namespace App\Command\Console;

use App\Command\GetBGGData;
use App\Command\GetBGGDataHandler;
use App\Exception\NoBoardGameAddedException;
use Exception;
use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputArgument;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;

class SyncBGGData extends Command
{
    /** @var GetBGGDataHandler */
    private $dataHandler;

    /**
     * @param GetBGGDataHandler $dataHandler
     * @param null $name
     */
    public function __construct(GetBGGDataHandler $dataHandler, $name = null)
    {
        parent::__construct($name);

        $this->dataHandler = $dataHandler;
    }

    protected function configure()
    {
        $this
            ->setName('app:sync-bgg-data')
            ->setDescription('Imports BoardGameGeek data')
            ->addArgument('step', InputArgument::OPTIONAL, 'The amount of items to handle per request', 1000)
            ->addArgument('total', InputArgument::OPTIONAL, 'The amount of items to parse', 1000000);
    }

    /**
     * @param InputInterface $input
     * @param OutputInterface $output
     *
     * @return int|null|void
     */
    protected function execute(InputInterface $input, OutputInterface $output)
    {
        $output->writeln([
            'Importing BoardGameGeek data',
            '============================',
            '',
        ]);

        $total = (int) $input->getArgument('total');
        $step = (int) $input->getArgument('step');

        for ($i = 1; $i < $total; $i += $step) {
            $startTime = microtime(true);
            $rangeString = "$i to " . ($i + $step);
            try {
                $this->dataHandler->handle(new GetBGGData(range($i, $i + $step), true, true, true));
                $output->writeln("<info>Imported boardgames $rangeString</info>");
            } catch (Exception $e) {
                $output->writeln("<error>Failed to import boardgames $rangeString</error>");
                $output->writeln("<error>" . $e->getMessage() . "</error>");
                exit;
            }

            gc_collect_cycles();
            if ((microtime(true) - $startTime) > 1) {
                sleep(5);
            }
        }

        $output->writeln("<info>No more boardgames to import.</info>");
    }
}
