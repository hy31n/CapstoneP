<script>
    import { url } from "@roxi/routify"
  import { onMount } from "svelte";
  import { headerName } from "../store";
  import Feed from '@/components/Feed.svelte'

// textarea 변수
  let question;
  let loading = false;
  let message = [{
    'role':'assistant',
    'author':'AI',
    'text': '안녕하세요! 질문이 있으신가요?',
    'isLoading': false
  }];  

  onMount(() => {
    headerName.set('메인');
  });

//   submit 이벤트
  const handleSubmit = async() => {
    if(loading){
        return false;
    }
    if(question){
        const tempQuestion = question
        question=''

        message=message.concat([
            {
                'role':'user',
                'author':'User',
                'text': tempQuestion,
                'isLoading': false
            },{
                'role':'assistant',
                'author':'AI',
                'text': '',
                'isLoading': true
            }
        ]);
        loading = true;
        // API 요청하기 위한 데이터 생성
        const payload = new URLSearchParams();
        payload.append('question', tempQuestion);


        const response = await fetch('http://localhost:5000/api/chat',{
            method:'POST',
            body: payload,
            headers:{
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        })
        .then((response)=>response.json())
        .then((res)=> {
            // AI 답변 업데이트
            message.pop()
            message=message.concat([{
                'role':'assistant',
                'author':'AI',
                'text': res.data.answer,
                'isLoading': false
            }]);
            loading=false;
        })
        .catch((error)=>{
            console.error('error', error);
        });
    }else{
        alert('빈칸입니다!');
    }
  }
</script>

<div class="ui main text container">
    <div class="ui">
        <div class="ui feed segment scrolling">
            <!-- Feed 컴포넌트 생성 -->
             {#each message as message}
             <Feed message={message} />
             {/each}
        </div>
    </div>
        <!-- 기본 이벤트 무시하고 handleSubmit 실행 -->
        <form class="ui form" on:submit|preventDefault={handleSubmit}>
            <div class="field">
                <!-- 최상단에 선언한 question으로 값 공유 -->
                <textarea rows="2" name="question" bind:value={question}></textarea>
            </div>
            <!-- 이 버튼이 submit 버튼임을 명시 -->
            <button class="ui labeled submit icon button" type="submit">
                <i class="icon edit"></i> Send message 
            </button>
        </form>
    </div>
