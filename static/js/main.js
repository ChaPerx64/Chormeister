function dangerButtonClicked(e, link)
{
    if(confirm('Are you sure?')) {
        e.preventDefault();
        window.location.href = link
    }
}