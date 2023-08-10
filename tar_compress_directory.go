package main

import (
	"archive/tar"
	"compress/gzip"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"strings"
)

func createTarGz(sourceDir, targetFile string) error {
	tarFile, err := os.Create(targetFile)
	if err != nil {
		return err
	}
	defer tarFile.Close()

	gzipWriter := gzip.NewWriter(tarFile)
	defer gzipWriter.Close()

	tarWriter := tar.NewWriter(gzipWriter)
	defer tarWriter.Close()

	baseDir := filepath.Dir(sourceDir)
	return filepath.Walk(sourceDir, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}

		relPath, err := filepath.Rel(baseDir, path)
		if err != nil {
			return err
		}

		header, err := tar.FileInfoHeader(info, relPath)
		if err != nil {
			return err
		}

		if info.IsDir() {
			header.Name = relPath + "/"
		}

		if err := tarWriter.WriteHeader(header); err != nil {
			return err
		}

		if !info.Mode().IsRegular() {
			return nil
		}

		file, err := os.Open(path)
		if err != nil {
			return err
		}
		defer file.Close()

		_, err = io.Copy(tarWriter, file)
		return err
	})
}

func main() {
	sourceDir := "/path/to/source/directory"
	targetFile := "output.tar.gz"

	err := createTarGz(sourceDir, targetFile)
	if err != nil {
		fmt.Println("Error:", err)
		return
	}

	fmt.Println("Tar.gz file created:", targetFile)
}
