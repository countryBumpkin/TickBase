class dcxml:

    _dspace_template_keys = [
            'contributor',
            'date.accessioned',
            'date.available',
            'date.issued',
            'identifier',
            'identifier.citation',
            'identifier.govdoc',
            'identifier.isbn',
            'identifier.issn',
            'identifier.ismn',
            'identifier.other',
            'identifier.uri',
            'description',
            'description.abstract',
            'description.provenance',
            'description.sponsorship',
            'format',
            'format.extent',
            'format.medium',
            'format.mimetype',
            'language.iso',
            'publisher',
            'subject',
            'title',
            'title.alternative',
            'type'
    ]

    def __init__(self, dictionary={}):

        self._dc = {}

        for key in dictionary.keys():
            if key in self._dspace_template_keys:
                self._dc[key] = dictionary[key]

    # Allows object to be formatted as string
    def __str__(self):
        return self.tostring()

    # Convert dictionary to xml string
    def tostring(self):
        str = '<dublin_core>'

        for key in self._dc.keys():
            kparts = key.split('.') # create array of terms, first is the key, second is qualifier
            element = kparts[0]

            if len(kparts) > 1:
                qualifier = kparts[1]
            else:
                qualifier = 'none'

            line = '\n\t<dcvalue element=\"{}\" qualifier="{}">{}</dcvalue>'.format(element, qualifier, self._dc[key])
            str = str + line

        str = str + '\n</dublin_core>'
        return str
