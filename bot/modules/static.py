WelcomeText = \
"""
Hello %(first_name)s, send me a video or any other file to get stream, download and retrieval link of it.
Also you can add me to your channel to attach links of any media file on that post.
"""

UserInfoText = \
"""
**First Name:**
`{sender.first_name}`

**Last Name:**
`{sender.last_name}`

**User ID:**
`{sender.id}`

**Username:**
`@{sender.username}`
"""

FileLinksText = \
"""
**🔗 Links successfully generated!**

**📥 Download Link:**
`%(dl_link)s`

"""

MediaLinksText = \
"""
**🔗 Links successfully generated!**

**📥 Download Link:**
`%(dl_link)s`

**🖥 Stream Link:**
`%(stream_link)s`

"""

InvalidQueryText = \
"""
Your url is invalid.
"""

MessageNotExist = \
"""
File is missing in database.
"""

LinkRevokedText = \
"""
File Successfully deleted.
"""

InvalidPayloadText = \
"""
Invalid payload.
"""

MediaTypeNotSupportedText = \
"""
Sorry, this file is not supported.
"""
