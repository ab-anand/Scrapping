<?php

namespace App\Command;

class GetBGGData
{
    /** @var int */
    private $ids;

    /** @var bool */
    private $resizeImage;

    /** @var bool */
    private $exportJson;

    /** @var bool */
    private $exportXml;

    /**
     * @param array $id
     * @param bool $resizeImage
     * @param bool $exportJson
     * @param bool $exportXml
     */
    public function __construct(array $ids, bool $resizeImage, bool $exportJson, bool $exportXml)
    {
        $this->ids = $ids;
        $this->resizeImage = $resizeImage;
        $this->exportJson = $exportJson;
        $this->exportXml = $exportXml;
    }

    /**
     * @return int
     */
    public function getIds(): array
    {
        return $this->ids;
    }

    /**
     * @return bool
     */
    public function isResizeImage(): bool
    {
        return $this->resizeImage;
    }

    /**
     * @return bool
     */
    public function isExportJson(): bool
    {
        return $this->exportJson;
    }

    /**
     * @return bool
     */
    public function isExportXml(): bool
    {
        return $this->exportXml;
    }
}
