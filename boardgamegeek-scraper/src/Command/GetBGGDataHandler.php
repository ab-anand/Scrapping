<?php

namespace App\Command;

use App\Exception\BoardGameGeekUnavailableException;
use App\ValueObject\BoardGame;
use Exception;
use GuzzleHttp\Client;
use SimpleXMLElement;

class GetBGGDataHandler
{
    /** @var string */
    private $rootDir;

    /** @var string */
    private $bggEndpoint;

    /**
     * @param string $rootDir
     * @param string $bggEndpoint
     */
    public function __construct(
        string $rootDir,
        string $bggEndpoint
    ) {
        $this->rootDir = $rootDir;
        $this->bggEndpoint = $bggEndpoint;
    }

    /**
     * @param GetBGGData $data
     */
    public function handle(GetBGGData $data): void
    {
        $boardGames = $this->getData($data->getIds());

        foreach ($boardGames as $boardGame) {
            $boardGame = $this->copyImageToLocal($boardGame);
            $this->saveXML($boardGame);
        }
    }

    /**
     * @param BoardGame $boardGame
     * @param bool $override
     */
    private function saveXML(BoardGame $boardGame): void
    {
        $cachedXMLPath = $this->rootDir . '/../public/boardgames/' . $boardGame->getId() . '/data.xml';

        $this->saveDataToFile(
            $cachedXMLPath,
            $boardGame->toXML()->asXML()
        );
    }

    /**
     * @param BoardGame $boardGame
     *
     * @return BoardGame
     */
    private function copyImageToLocal(BoardGame $boardGame): BoardGame
    {
        if (!empty($boardGame->getImage())) {
            $extension = array_reverse(explode('.', $boardGame->getImage()))[0];
            $cachedImagePath = $this->rootDir . '/../public/boardgames/' . $boardGame->getId() . '/image.' . $extension;
        }

        if (!empty($boardGame->getImage()) && file_exists($cachedImagePath) && !filesize($cachedImagePath)) {
            unlink($cachedImagePath);
        }

        if ((!empty($boardGame->getImage()) && !file_exists($cachedImagePath))) {
            $curl = curl_init();
            curl_setopt($curl, CURLOPT_URL, $boardGame->getImage());
            curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
            $result = curl_exec($curl);
            curl_close($curl);

            if (!empty($result)) {
                $this->saveDataToFile(
                    $cachedImagePath,
                    $result
                );
            }
        }

        if (empty($boardGame->getImage()) || !file_exists($cachedImagePath)) {
            return new BoardGame(
                $boardGame->getId(),
                $boardGame->getName(),
                $boardGame->getDescription(),
                null
            );
        }

        return new BoardGame(
            $boardGame->getId(),
            $boardGame->getName(),
            $boardGame->getDescription(),
            '/boardgames/' . $boardGame->getId() . '/image.'. $extension
        );
    }

    /**
     * @param array $ids
     *
     * @return BoardGame
     */
    private function getData(array $ids): array
    {
        $boardgames = [];

        try {
            $data = $this->getCachedData($ids);
            if (empty($data)) {
                $data = $this->getBoardGameGeekData($ids);
            }
        } catch (BoardGameGeekUnavailableException $exception) {
            $this->removeBoardGameGeekData($ids);
            sleep(60);

            return $this->getData($ids);
        }

        try {
            foreach ($data->children() as $child) {
                $boardgames[] = new BoardGame(
                    (int) $child->attributes()['id'],
                    $child->children()->name->attributes()['value'],
                    $child->children()->description,
                    $child->children()->image
                );
            }
        } catch (Exception $exception) {
            $this->removeBoardGameGeekData($ids);

            if (count($ids) !== 1) {
                $chunks = array_chunk($ids, ceil(count($ids) / 2));
                $boardgames = array_merge(
                    $this->getData($chunks[0]),
                    $this->getData($chunks[1])
                );
            }
        }

        return $boardgames;
    }

    /**
     * @param array $ids
     *
     * @return null|SimpleXMLElement
     */
    private function getCachedData(array $ids): ?SimpleXMLElement
    {
        $id = implode(',', $ids);
        $hash = md5($id);
        $cachedDataPath = $this->rootDir . '/../var/cache/boardgames/' . substr($hash, 0, 3) . '/' . $hash . '/raw-data.xml';

        if (file_exists($cachedDataPath)) {
            return simplexml_load_string(
                file_get_contents($cachedDataPath)
            );
        }

        return null;
    }

    private function removeBoardGameGeekData(array $ids): void
    {
        $id = implode(',', $ids);
        $hash = md5($id);
        $cachedDataPath = $this->rootDir . '/../var/cache/boardgames/' . substr($hash, 0, 3) . '/' . $hash . '/raw-data.xml';

        if (file_exists($cachedDataPath)) {
            unlink($cachedDataPath);
        }
    }

    /**
     * @param array $ids
     *
     * @return SimpleXMLElement
     *
     * @throws BoardGameGeekUnavailableException
     */
    private function getBoardGameGeekData(array $ids): SimpleXMLElement
    {
        $id = implode(',', $ids);
        $hash = md5($id);
        $cachedDataPath = $this->rootDir . '/../var/cache/boardgames/' . substr($hash, 0, 3) . '/' . $hash . '/raw-data.xml';

        $url = $this->bggEndpoint . 'thing?type=boardgame&id=' . $id;

        $client = new Client();
        $response = $client->get($url);

        if ($response->getStatusCode() === 429) {
            throw BoardGameGeekUnavailableException::create();
        }

        $data = simplexml_load_string($response->getBody());

        if ($data->children()->count()) {
            $this->saveDataToFile(
                $cachedDataPath,
                $data->asXML()
            );
        }

        return $data;
    }

    /**
     * @param string $dir
     * @param string $contents
     */
    private function saveDataToFile(string $dir, string $contents): void
    {
        if (file_exists($dir)) {
            unlink($dir);
        }

        $parts = explode('/', $dir);
        $file = array_pop($parts);
        $dir = '';
        foreach ($parts as $part) {
            if (!is_dir($dir .= "/$part")) {
                mkdir($dir);
            }
        }
        file_put_contents("$dir/$file", $contents);
    }
}
