using System.Threading.Tasks;

namespace RMS.services.Interfaces
{
    public interface IImageService
    {
        public Task<string> UploadDataURI(string dataURI, string fileName);

        public Task<string> DownloadImageURL(string fileId);

        public Task DeleteImageURL(string fileId);
    }
}