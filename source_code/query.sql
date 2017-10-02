select Id, PostTypeId, ParentId, Body, Tags
from Posts
where Id in (
    select top 500 Id
    from Posts
    where
        AnswerCount >= 1 -- at least 2 posts 
        and Tags like '%<python>%' -- python in tags
        and CreationDate <= '2017-09-01'
    )
    or ParentId in (
    select top 500 Id
    from Posts
    where
        AnswerCount >= 1 -- at least 2 posts 
        and Tags like '%<python>%' -- python in tags
        and CreationDate <= '2017-09-01'
    )
;