package main

import (
	"archive/tar"
	"compress/gzip"
	"fmt"
	"io"
	"os"
	"path/filepath"
)

func addFileToTar(writer *tar.Writer, path, name string, info os.FileInfo) error {
	file, err := os.Open(path)
	if err != nil {
		return err
	}
	defer file.Close()

	header, err := tar.FileInfoHeader(info, "")
	if err != nil {
		return err
	}
	header.Name = name

	if err := writer.WriteHeader(header); err != nil {
		return err
	}

	_, err = io.Copy(writer, file)
	return err
}

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

	info, err := os.Stat(sourceDir)
	if err != nil {
		return err
	}

	baseDir := filepath.Base(sourceDir)

	if !info.IsDir() {
		return fmt.Errorf("sourceDir must be a directory")
	}

	filepath.Walk(sourceDir, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}

		relPath, err := filepath.Rel(sourceDir, path)
		if err != nil {
			return err
		}

		if relPath == "." {
			return nil
		}

		targetPath := filepath.Join(baseDir, relPath)
		if info.IsDir() {
			targetPath += "/"
		}

		return addFileToTar(tarWriter, path, targetPath, info)
	})

	return nil
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
