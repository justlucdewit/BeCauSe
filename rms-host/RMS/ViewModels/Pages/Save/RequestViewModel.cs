using System;

namespace RMS.ViewModels.Pages.Save
{
    public class RequestViewModel
    {
        public int? Id { get; set; }

        public string MarkdownContent { get; set; }

        public string Name { get; set; }

        public int Order { get; set; }

        public string UrlName { get; set; }

        public bool UserMade { get; set; }
        
        public string SpecialPageId { get; set; }
    }
}