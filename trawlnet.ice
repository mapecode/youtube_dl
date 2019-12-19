// Trawlent 3rd phase: the final system

module TrawlNet {
  exception GeneralError {
      string reason;
  };

  exception DownloadError extends GeneralError {};
  exception TransferError extends GeneralError {};

  struct FileInfo {
    string name;
    string hash;
  };

  sequence<FileInfo> FileList;

  interface Transfer {
    string recv(int size);
    void close();
    void destroy();
  };

  interface TransferFactory {
    Transfer* create(string fileName);
  };

  interface Downloader {
    FileInfo addDownloadTask(string url)
      throws DownloadError;
    void destroy();
  };

  interface DownloaderFactory {
    Downloader* create();
  };

  interface Orchestrator {
    FileList getFileList();
    Transfer* getFile(string name);
    void announce(Orchestrator* other);
    FileInfo downloadTask(string url)
      throws DownloadError;
  };

  interface OrchestratorEvent {
    void hello(Orchestrator* me);
  };

  interface UpdateEvent {
    void newFile(FileInfo file);
  };
};