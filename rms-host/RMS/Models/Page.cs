using System;

namespace RMS.Models
{
    public class Page
    {
        public int Id { get; set; }

        public string Name { get; set; }
        
        public string MarkdownContent { get; set; }

        public string URLName { get; set; }

        public int Order { get; set; }

        public int CompanyId { get; set; }

        public bool UserMade { get; set; }

        public string SpecialPageId { get; set; }

        public virtual Company Company { get; set; }
    }
}