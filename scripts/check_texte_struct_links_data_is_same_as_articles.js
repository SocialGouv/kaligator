db.textes.aggregate([
  {$project: {"STRUCT": 1, _id: 0}},
  {$unwind: "$STRUCT"},
  {$match: {'STRUCT._type': "LIEN_ART"}},
  {$lookup: {
      from: 'articles',
      localField: "STRUCT.id",
      foreignField: "META.META_COMMUN.ID",
      as: "articles"
  }},
  {$project: {
      'from_texte_struct_link': "$STRUCT",
      "from_article": {$arrayElemAt: ["$articles.META.META_SPEC.META_ARTICLE", 0]}
  }},
  {$project: {
      'from_texte_struct_link': {
          'debut': '$from_texte_struct_link.debut',
          'fin': '$from_texte_struct_link.fin',
          'etat': '$from_texte_struct_link.etat',
          'num': '$from_texte_struct_link.num',
      },
      'from_article': {
          'debut': '$from_article.DATE_DEBUT',
          'fin': '$from_article.DATE_FIN',
          'etat': '$from_article.ETAT',
          'num': '$from_article.NUM'
      },
  }},
  {$project: {from_texte_struct_link:1 , from_article: 1, cmp_value: {$cmp: ['$from_texte_struct_link', '$from_article']}}},
  {$match: {cmp_value: {$ne: 0}}}
])
